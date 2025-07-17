#!/bin/bash

# Helper functions
attime() { date +%Y-%m-%d %H:%M:%S; }
log_info() { echo -e "\033[1;32m$(attime) \033[1;34m[INFO]\033[1;0m\t$@"; }
log_debug() { echo -e "\033[1;32m$(attime) \033[1;35m[DEBUG]\033[1;0m\t$@"; }
log_error() { echo -e "\033[1;32m$(attime) \033[1;31m[ERROR]\033[1;0m\t$@"; }

# Helpful dates
CURRENT_MONTH=$(date +%m)
CURRENT_YEAR=$(date +%Y)

# Determine next run date (biannual: January and July)
if [[ "$CURRENT_MONTH" -eq 07 ]]; then
    NEXT_RUN=$(date -d "$CURRENT_YEAR-07-08 02:00" "+%Y-%m-%dT%H:%M")
elif [[ "$CURRENT_MONTH" -eq 01 ]]; then
    NEXT_RUN=$(date -d "$CURRENT_YEAR-01-08 02:00" "+%Y-%m-%dT%H:%M")
else
    # If not January or July, find the next occurrence
    if [[ "$CURRENT_MONTH" -lt 07 ]]; then
        NEXT_RUN=$(date -d "$CURRENT_YEAR-07-08 02:00" "+%Y-%m-%dT%H:%M")
    else
        NEXT_RUN=$(date -d "$((CURRENT_YEAR + 1))-01-08 02:00" "+%Y-%m-%dT%H:%M")
    fi
fi

# Check if this is a scheduled run or manual initialization
# If no argument provided, this is the initial manual run - just schedule
if [[ $# -eq 0 ]]; then
    log_info "Initializing biannual schedule. Next run: $NEXT_RUN"
    
    # Schedule the first automated run
    sbatch \
        --job-name="biannual_job" \
        --partition="gpu,standard" \
        --mail-type="ALL" \
        --mail-user="${USER}@pnc.com" \
        --time="6:00:00" \
        --nodes="1" \
        --ntasks="1" \
        --cpu-per-task="1" \
        --output="/projects/${USER}/logs/dsi/prules_pmt_prt_logs/sbatch_%j.log" \
        --begin="$NEXT_RUN" \
        --dependency="$(SCHEDULE)" \
        --parsable \
        "$0" "SCHEDULED"
    
    log_info "Biannual job scheduled for $NEXT_RUN"
    exit 0
fi

# If we get here, this is a scheduled run - do the work AND schedule next run
log_info "Running scheduled biannual job"

# Schedule the NEXT occurrence before starting work
log_info "Scheduling next biannual run for $NEXT_RUN"

# Define variables for the actual work
SLURM_DIR="/projects/${USER}/repos/dsi/dsi-pme-prt-rules/slurm/prt_data_biannual"
PRT_BASE_FILE="${SLURM_DIR}/sbatch_prules_prt_rule_base.sh"
PRT_COMPLETE_FILE="${SLURM_DIR}/sbatch_prules_prt_rule_complete.sh"

# Submit next occurrence
NEXT_JOB_ID=$(sbatch \
    --job-name="biannual_job" \
    --partition="gpu,standard" \
    --mail-type="ALL" \
    --mail-user="${USER}@pnc.com" \
    --time="6:00:00" \
    --nodes="1" \
    --ntasks="1" \
    --cpu-per-task="1" \
    --output="/projects/${USER}/logs/dsi/prules_pmt_prt_logs/sbatch_%j.log" \
    --begin="$NEXT_RUN" \
    --parsable \
    "$0" "SCHEDULED")

log_info "Next biannual job scheduled with ID: $NEXT_JOB_ID for $NEXT_RUN"

# Now do the actual work
log_info "Starting biannual data processing..."

# Submit PRT Base job
PRT_BASE_ID=$(sbatch --dependency="afterok:${PRT_BASE_FILE}")
log_info "Submitted PRT Base Job: \$job_id = $PRT_BASE_ID; \$begin ${SCHEDULE}"

DEPS="afterok:${PRT_BASE_ID}"

# Submit PRT Complete job  
PRT_COMPLETE_ID=$(sbatch --dependency="$DEPS" "${PRT_COMPLETE_FILE}")
log_info "Submitted PRT Complete Job: \$job_id = $PRT_COMPLETE_ID; \$begin ${SCHEDULE}"

log_info "Biannual job workflow submitted successfully"
