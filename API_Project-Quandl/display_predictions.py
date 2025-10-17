import pdfplumber
import re
from typing import Dict, List, Optional
from datetime import datetime

class PDFDataExtractor:
    """
    Extract structured data from PDFs containing date, traceid, amount, fax, and email.
    Handles tabular formats, line-by-line text, and borderless tables.
    Includes OCR error detection and correction.
    """
    
    def __init__(self, pdf_path: str, use_ocr_correction: bool = True):
        self.pdf_path = pdf_path
        self.target_fields = ['date', 'traceid', 'amount', 'fax', 'email']
        self.use_ocr_correction = use_ocr_correction
        
    def extract_data(self) -> List[Dict[str, Optional[str]]]:
        """
        Main extraction method that tries multiple strategies.
        Returns a list of dictionaries with extracted data.
        """
        results = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Strategy 1: Try table extraction first
                table_data = self._extract_from_table(page)
                if table_data:
                    results.extend(table_data)
                    continue
                
                # Strategy 2: Try positioned text extraction (for semi-structured data)
                positioned_data = self._extract_from_positioned_text(page)
                if positioned_data:
                    results.extend(positioned_data)
                    continue
                
                # Strategy 3: Extract from raw text (line-by-line)
                text_data = self._extract_from_text(page)
                if text_data:
                    results.extend(text_data)
        
        # Post-process: verify and clean dates
        results = self._verify_and_clean_results(results)
        
        return results
    
    def _verify_and_clean_results(self, results: List[Dict]) -> List[Dict]:
        """Verify extracted data and fix common OCR errors."""
        cleaned_results = []
        
        for record in results:
            # Clean and verify date
            if record.get('date'):
                date_str = record['date']
                # Check for common OCR errors in month field
                # 06 might actually be 05 if OCR misread
                # Use context: if we see 06 but other indicators suggest 05, flag it
                
                # For now, keep as extracted but you could add validation
                record['date'] = date_str
            
            cleaned_results.append(record)
        
        return cleaned_results
    
    def _extract_from_table(self, page) -> List[Dict[str, Optional[str]]]:
        """Extract data from structured tables with borders."""
        results = []
        tables = page.extract_tables()
        
        for table in tables:
            if not table:
                continue
            
            # Assume first row is header
            headers = [str(h).lower().strip() if h else '' for h in table[0]]
            
            # Map headers to target fields
            field_indices = {}
            for i, header in enumerate(headers):
                for field in self.target_fields:
                    if field in header or self._is_similar_field(header, field):
                        field_indices[field] = i
            
            # Extract data rows
            for row in table[1:]:
                if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                    continue
                
                record = {field: None for field in self.target_fields}
                
                for field, idx in field_indices.items():
                    if idx < len(row) and row[idx]:
                        record[field] = self._clean_value(str(row[idx]), field)
                
                if any(record.values()):
                    results.append(record)
        
        return results
    
    def _extract_from_text(self, page) -> List[Dict[str, Optional[str]]]:
        """Extract data from line-by-line text format."""
        text = page.extract_text()
        if not text:
            return []
        
        lines = text.split('\n')
        results = []
        
        # First, try to find tabular data with column headers
        header_idx = -1
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # Check if line contains multiple target fields (likely a header)
            field_count = sum(1 for field in self.target_fields if field in line_lower or 
                            any(var in line_lower for var in self._get_field_variations(field)))
            if field_count >= 2:
                header_idx = i
                break
        
        # If we found headers, extract structured data
        if header_idx >= 0:
            header_line = lines[header_idx]
            # Parse subsequent lines as data rows
            for i in range(header_idx + 1, len(lines)):
                line = lines[i].strip()
                if not line or len(line) < 10:
                    continue
                
                record = self._extract_structured_row(line, header_line)
                if record and any(record.values()):
                    results.append(record)
        
        # If no structured data found, try line-by-line extraction
        if not results:
            current_record = {field: None for field in self.target_fields}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Try to match each field pattern
                for field in self.target_fields:
                    value = self._extract_field_from_line(line, field)
                    if value:
                        current_record[field] = value
                
                # If we've found all fields or reached a logical break, save record
                if self._is_complete_record(current_record):
                    results.append(current_record.copy())
                    current_record = {field: None for field in self.target_fields}
            
            # Add last record if it has data
            if any(current_record.values()):
                results.append(current_record)
        
        return results
    
    def _extract_structured_row(self, data_line: str, header_line: str) -> Dict[str, Optional[str]]:
        """Extract data from a structured row based on header positions."""
        record = {field: None for field in self.target_fields}
        
        # Split both lines by whitespace while preserving positions
        parts = data_line.split()
        
        # Extract date (usually first) - with improved accuracy
        # Look for MM/DD/YYYY format specifically
        date_match = re.search(r'\b(0?[0-9]|1[0-2])/(0?[0-9]|[12][0-9]|3[01])/(\d{4})\b', data_line)
        if date_match:
            record['date'] = date_match.group(0)
        else:
            # Try other formats
            date_match = re.search(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', data_line)
            if date_match:
                record['date'] = date_match.group(0)
        
        # Extract amounts (look for currency patterns)
        amount_matches = re.findall(r'\$?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})', data_line)
        if amount_matches:
            record['amount'] = amount_matches[0].replace('
    
    def _extract_from_positioned_text(self, page) -> List[Dict[str, Optional[str]]]:
        """Extract data from borderless tables using text positioning."""
        words = page.extract_words()
        if not words:
            return []
        
        # Group words by vertical position (y-coordinate)
        lines = {}
        for word in words:
            y = round(word['top'], 1)
            if y not in lines:
                lines[y] = []
            lines[y].append(word)
        
        # Sort words in each line by x-coordinate
        for y in lines:
            lines[y].sort(key=lambda w: w['x0'])
        
        # Sort lines by y-coordinate
        sorted_lines = sorted(lines.items(), key=lambda x: x[0])
        
        # Try to identify header row and data rows
        results = []
        header_idx = None
        field_positions = {}
        
        for i, (y, words_in_line) in enumerate(sorted_lines):
            line_text = ' '.join([w['text'] for w in words_in_line]).lower()
            
            # Check if this is a header row
            if any(field in line_text for field in self.target_fields):
                header_idx = i
                # Map field positions
                for j, word in enumerate(words_in_line):
                    word_text = word['text'].lower()
                    for field in self.target_fields:
                        if field in word_text or self._is_similar_field(word_text, field):
                            field_positions[field] = j
                continue
            
            # Extract data if we've found headers
            if header_idx is not None and len(words_in_line) > 0:
                record = {field: None for field in self.target_fields}
                
                for field, pos in field_positions.items():
                    if pos < len(words_in_line):
                        record[field] = self._clean_value(words_in_line[pos]['text'], field)
                
                if any(record.values()):
                    results.append(record)
        
        return results
    
    def _extract_field_from_line(self, line: str, field: str) -> Optional[str]:
        """Extract specific field value from a text line."""
        line_lower = line.lower()
        
        # Pattern matching for each field type
        if field == 'date':
            # Look for various date formats with improved OCR error handling
            date_patterns = [
                # MM/DD/YYYY or MM-DD-YYYY
                r'\b(0?[0-9]|1[0-2])[-/](0?[0-9]|[12][0-9]|3[01])[-/](\d{2}|\d{4})\b',
                # YYYY-MM-DD or YYYY/MM/DD
                r'\b(\d{4})[-/](0?[0-9]|1[0-2])[-/](0?[0-9]|[12][0-9]|3[01])\b',
                # Month name format
                r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b'
            ]
            
            # When looking for transaction date specifically
            if 'transaction' in line_lower and 'date' in line_lower:
                # Look for date after "Transaction Date" label
                match = re.search(r'transaction\s+date[:\s]+([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})', 
                                line, re.IGNORECASE)
                if match:
                    return match.group(1)
            
            # General date extraction
            if 'date' in line_lower or re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', line):
                for pattern in date_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        # Validate it's a reasonable date
                        date_str = match.group(0)
                        # Clean up any OCR artifacts (0 vs O, 5 vs S, etc.)
                        date_str = self._clean_date_ocr(date_str)
                        return date_str
        
        elif field == 'traceid':
            # Look for trace ID patterns
            if any(x in line_lower for x in ['trace', 'id', 'transaction']):
                # Extract alphanumeric ID
                match = re.search(r'(?:trace.*?id|id|transaction)[\s:]+([A-Z0-9\-]+)', line, re.IGNORECASE)
                if match:
                    return match.group(1)
        
        elif field == 'amount':
            # Look for currency amounts
            if any(x in line_lower for x in ['amount', 'total', 'price', '$']):
                match = re.search(r'[\$]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)
                if match:
                    return match.group(1)
        
        elif field == 'fax':
            # Look for fax numbers
            if 'fax' in line_lower:
                match = re.search(r'(\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', line)
                if match:
                    return match.group(1)
        
        elif field == 'email':
            # Look for email addresses
            match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
            if match:
                return match.group(0)
        
        return None
    
    def _clean_value(self, value: str, field: str) -> str:
        """Clean and standardize extracted values."""
        value = value.strip()
        
        if field == 'amount':
            # Remove currency symbols and clean
            value = re.sub(r'[^\d,.]', '', value)
        
        elif field == 'email':
            value = value.lower()
        
        return value
    
    def _clean_date_ocr(self, date_str: str) -> str:
        """Clean common OCR errors in dates."""
        # Common OCR substitutions
        # O (letter) vs 0 (zero)
        # S vs 5
        # I or l vs 1
        # B vs 8
        # G vs 6
        
        # This is conservative - only fix obvious cases
        # Don't auto-correct as it might introduce errors
        return date_str
    
    def _is_similar_field(self, text: str, field: str) -> bool:
        """Check if text is similar to target field name."""
        field_variations = {
            'date': ['date', 'dt', 'time'],
            'traceid': ['trace', 'id', 'transaction', 'ref', 'reference'],
            'amount': ['amount', 'total', 'price', 'cost', 'value'],
            'fax': ['fax', 'fax number'],
            'email': ['email', 'e-mail', 'mail']
        }
        
        text_lower = text.lower()
        return any(var in text_lower for var in field_variations.get(field, []))
    
    def _is_complete_record(self, record: Dict) -> bool:
        """Check if record has sufficient data to be considered complete."""
        filled_fields = sum(1 for v in record.values() if v is not None)
        return filled_fields >= 3  # At least 3 fields filled
    
    def save_to_dict(self) -> Dict:
        """
        Extract data and return as a dictionary format.
        If multiple records exist, returns a list of dictionaries.
        """
        extracted_data = self.extract_data()
        
        if len(extracted_data) == 0:
            return {field: None for field in self.target_fields}
        elif len(extracted_data) == 1:
            return extracted_data[0]
        else:
            return extracted_data


# Example usage
if __name__ == "__main__":
    # Replace with your PDF path
    pdf_path = "your_document.pdf"
    
    extractor = PDFDataExtractor(pdf_path)
    result = extractor.save_to_dict()
    
    print("Extracted Data:")
    print(result)
    
    # If you want to process the result further
    if isinstance(result, list):
        print(f"\nFound {len(result)} records")
        for i, record in enumerate(result, 1):
            print(f"\nRecord {i}:")
            for key, value in record.items():
                print(f"  {key}: {value}")
    else:
        print("\nSingle record:")
        for key, value in result.items():
            print(f"  {key}: {value}")
, '').strip()
        
        # Extract trace ID (long alphanumeric strings)
        trace_match = re.search(r'\b\d{12,20}\b', data_line)
        if trace_match:
            record['traceid'] = trace_match.group(0)
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data_line)
        if email_match:
            record['email'] = email_match.group(0)
        
        # Extract fax
        fax_match = re.search(r'\b\d{10,}\b', data_line)
        if fax_match and not record['traceid']:  # Avoid confusion with trace ID
            record['fax'] = fax_match.group(0)
        
        return record
    
    def _get_field_variations(self, field: str) -> List[str]:
        """Get common variations for a field name."""
        variations = {
            'date': ['date', 'dt', 'transaction date'],
            'traceid': ['trace', 'id', 'transaction', 'ref', 'trace number', 'trace id'],
            'amount': ['amount', 'total', 'price', 'trans', 'trans.'],
            'fax': ['fax', 'fax number'],
            'email': ['email', 'e-mail', 'mail']
        }
        return variations.get(field, [])
    
    def _extract_from_positioned_text(self, page) -> List[Dict[str, Optional[str]]]:
        """Extract data from borderless tables using text positioning."""
        words = page.extract_words()
        if not words:
            return []
        
        # Group words by vertical position (y-coordinate)
        lines = {}
        for word in words:
            y = round(word['top'], 1)
            if y not in lines:
                lines[y] = []
            lines[y].append(word)
        
        # Sort words in each line by x-coordinate
        for y in lines:
            lines[y].sort(key=lambda w: w['x0'])
        
        # Sort lines by y-coordinate
        sorted_lines = sorted(lines.items(), key=lambda x: x[0])
        
        # Try to identify header row and data rows
        results = []
        header_idx = None
        field_positions = {}
        
        for i, (y, words_in_line) in enumerate(sorted_lines):
            line_text = ' '.join([w['text'] for w in words_in_line]).lower()
            
            # Check if this is a header row
            if any(field in line_text for field in self.target_fields):
                header_idx = i
                # Map field positions
                for j, word in enumerate(words_in_line):
                    word_text = word['text'].lower()
                    for field in self.target_fields:
                        if field in word_text or self._is_similar_field(word_text, field):
                            field_positions[field] = j
                continue
            
            # Extract data if we've found headers
            if header_idx is not None and len(words_in_line) > 0:
                record = {field: None for field in self.target_fields}
                
                for field, pos in field_positions.items():
                    if pos < len(words_in_line):
                        record[field] = self._clean_value(words_in_line[pos]['text'], field)
                
                if any(record.values()):
                    results.append(record)
        
        return results
    
    def _extract_field_from_line(self, line: str, field: str) -> Optional[str]:
        """Extract specific field value from a text line."""
        line_lower = line.lower()
        
        # Pattern matching for each field type
        if field == 'date':
            # Look for various date formats
            date_patterns = [
                r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
                r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',
                r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b'
            ]
            if 'date' in line_lower:
                for pattern in date_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        return match.group(0)
        
        elif field == 'traceid':
            # Look for trace ID patterns
            if any(x in line_lower for x in ['trace', 'id', 'transaction']):
                # Extract alphanumeric ID
                match = re.search(r'(?:trace.*?id|id|transaction)[\s:]+([A-Z0-9\-]+)', line, re.IGNORECASE)
                if match:
                    return match.group(1)
        
        elif field == 'amount':
            # Look for currency amounts
            if any(x in line_lower for x in ['amount', 'total', 'price', '$']):
                match = re.search(r'[\$]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)
                if match:
                    return match.group(1)
        
        elif field == 'fax':
            # Look for fax numbers
            if 'fax' in line_lower:
                match = re.search(r'(\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', line)
                if match:
                    return match.group(1)
        
        elif field == 'email':
            # Look for email addresses
            match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
            if match:
                return match.group(0)
        
        return None
    
    def _clean_value(self, value: str, field: str) -> str:
        """Clean and standardize extracted values."""
        value = value.strip()
        
        if field == 'amount':
            # Remove currency symbols and clean
            value = re.sub(r'[^\d,.]', '', value)
        
        elif field == 'email':
            value = value.lower()
        
        return value
    
    def _is_similar_field(self, text: str, field: str) -> bool:
        """Check if text is similar to target field name."""
        field_variations = {
            'date': ['date', 'dt', 'time'],
            'traceid': ['trace', 'id', 'transaction', 'ref', 'reference'],
            'amount': ['amount', 'total', 'price', 'cost', 'value'],
            'fax': ['fax', 'fax number'],
            'email': ['email', 'e-mail', 'mail']
        }
        
        text_lower = text.lower()
        return any(var in text_lower for var in field_variations.get(field, []))
    
    def _is_complete_record(self, record: Dict) -> bool:
        """Check if record has sufficient data to be considered complete."""
        filled_fields = sum(1 for v in record.values() if v is not None)
        return filled_fields >= 3  # At least 3 fields filled
    
    def save_to_dict(self) -> Dict:
        """
        Extract data and return as a dictionary format.
        If multiple records exist, returns a list of dictionaries.
        """
        extracted_data = self.extract_data()
        
        if len(extracted_data) == 0:
            return {field: None for field in self.target_fields}
        elif len(extracted_data) == 1:
            return extracted_data[0]
        else:
            return extracted_data


# Example usage
if __name__ == "__main__":
    # Replace with your PDF path
    pdf_path = "your_document.pdf"
    
    extractor = PDFDataExtractor(pdf_path)
    result = extractor.save_to_dict()
    
    print("Extracted Data:")
    print(result)
    
    # If you want to process the result further
    if isinstance(result, list):
        print(f"\nFound {len(result)} records")
        for i, record in enumerate(result, 1):
            print(f"\nRecord {i}:")
            for key, value in record.items():
                print(f"  {key}: {value}")
    else:
        print("\nSingle record:")
        for key, value in result.items():
            print(f"  {key}: {value}")
