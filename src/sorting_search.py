def merge_sort(transactions, key=lambda t: t.risk_score, reverse=False):
    """
    Sorts a list of Transaction objects using merge sort.
    key: function that extracts the value to sort by (default: risk_score)
    reverse: True for descending order (e.g., highest risk first)
    """
    if len(transactions) <= 1:
        return transactions

    mid = len(transactions) // 2
    left = merge_sort(transactions[:mid], key, reverse)
    right = merge_sort(transactions[mid:], key, reverse)

    return _merge(left, right, key, reverse)


def _merge(left, right, key, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        take_left = key(left[i]) <= key(right[j])
        if reverse:
            take_left = key(left[i]) >= key(right[j])

        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search_by_amount(sorted_transactions, target_amount):
    """
    Searches a list of Transaction objects (already sorted by amount, ascending)
    for a transaction matching target_amount. Returns the Transaction or None.
    """
    low, high = 0, len(sorted_transactions) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_amount = sorted_transactions[mid].amount

        if mid_amount == target_amount:
            return sorted_transactions[mid]
        elif mid_amount < target_amount:
            low = mid + 1
        else:
            high = mid - 1

    return None


def linear_search_by_amount(transactions, target_amount):
    """Naive O(n) search - kept here purely to benchmark against binary search."""
    for t in transactions:
        if t.amount == target_amount:
            return t
    return None


if __name__ == "__main__":
    from transaction import Transaction

    txns = [
        Transaction("T001", "U001", 5000, "2025-01-15T10:00:00", "Chennai", "D01", "Amazon"),
        Transaction("T002", "U002", 15000, "2025-01-15T10:05:00", "Mumbai", "D02", "Flipkart"),
        Transaction("T003", "U001", 200, "2025-01-15T10:10:00", "Chennai", "D01", "Zomato"),
        Transaction("T004", "U003", 90000, "2025-01-15T10:15:00", "Delhi", "D03", "Croma"),
    ]

    txns[0].risk_score = 20
    txns[1].risk_score = 70
    txns[2].risk_score = 10
    txns[3].risk_score = 95

    sorted_by_risk = merge_sort(txns, key=lambda t: t.risk_score, reverse=True)
    print("Sorted by risk (highest first):")
    for t in sorted_by_risk:
        print(" ", t)

    sorted_by_amount = merge_sort(txns, key=lambda t: t.amount)
    print("\nSorted by amount (ascending):")
    for t in sorted_by_amount:
        print(" ", t)

    found = binary_search_by_amount(sorted_by_amount, 15000)
    print("\nBinary search for amount=15000:", found)

    not_found = binary_search_by_amount(sorted_by_amount, 99999)
    print("Binary search for amount=99999:", not_found)