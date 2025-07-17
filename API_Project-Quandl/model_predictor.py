# Get current month to determine which submit file to run
CURRENT_MONTH=$(date +%m)

log_info "Current month: $CURRENT_MONTH"
log_info "Queuing next set of jobs"

# Only run the appropriate submit file based on current month
if [ "$CURRENT_MONTH" == "01" ]; then
    log_info "Running January submission file"
    bash "${SUBMIT_FILE_01}"
elif [ "$CURRENT_MONTH" == "07" ]; then
    log_info "Running July submission file"  
    bash "${SUBMIT_FILE_07}"
else
    log_info "Not January or July - no additional jobs to queue"
fi

log_info "Finished queuing next job"
