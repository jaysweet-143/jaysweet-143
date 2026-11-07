def execute_binary_search(sorted_vault, target_amount):
    low_index = 0
    high_index = len(sorted_vault) - 1
    
    operation_count = 0
    
    while low_index <= high_index:
          operation_count += 1
          mid_index = (low_index + high_index) // 2
          mid_record = sorted_vault[mid_index]

          #If mid_record equals target record, end loop and return the value
          if mid_record["amount"] == target_amount:
             return mid_record, operation_count
          #Else if mid_record is greater than target record, shift search to the left portion
          elif mid_record["amount"] > target_amount:
             high_index = mid_index - 1  
          #Else if mid_record is smaller than target record, shift search to the right portion
          else:
             low_index = mid_index + 1
    # If the loop ends without a match, return None along with the final step count
    return None, operation_count   

# The main execution engine block
if __name__ == "__main__":
    # CRITICAL DATA PRE-REQUISITE: Binary Search strictly requires a SORTED dataset array
    sorted_data_vault = [
        {"tx_id": "T1", "amount": 100},
        {"tx_id": "T2", "amount": 250},
        {"tx_id": "T3", "amount": 450},
        {"tx_id": "T4", "amount": 1140},
        {"tx_id": "T5", "amount": 2500},
        {"tx_id": "T6", "amount": 4999}
    ]
    target = 2500
    
    # Execute our binary search function
    found_record, steps = execute_binary_search(sorted_data_vault, target)
    
    print("BINARY SEARCH LIFECYCLE COMPLETE:")
    if found_record is not None:
        print(f"SUCCESS: Found Transaction {found_record['tx_id']}")
        print(f"Total Computational Checks Performed: {steps}")
    else:
        print("ALERT: Target amount not found in data vault.")