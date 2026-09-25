from sorting_search import merge_sort
from heap import RiskHeap


def run_menu(detector):
    """
    Console menu loop. Takes an already-populated FraudDetector
    (transactions already processed) and lets the user explore results.
    """
    while True:
        print("\n" + "=" * 50)
        print("FRAUD DETECTION SYSTEM")
        print("=" * 50)
        print("1. Show all transactions")
        print("2. Show flagged transactions (ranked by risk)")
        print("3. Show top K riskiest transactions")
        print("4. Show suspicious device-sharing clusters (fraud rings)")
        print("5. Search transaction by amount range (AVL tree)")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            _show_all(detector)
        elif choice == "2":
            _show_flagged(detector)
        elif choice == "3":
            _show_top_k(detector)
        elif choice == "4":
            _show_fraud_rings(detector)
        elif choice == "5":
            _search_by_range(detector)
        elif choice == "6":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


def _show_all(detector):
    print(f"\nTotal transactions: {len(detector.all_transactions)}")
    for t in detector.all_transactions:
        print(f"  {t.txn_id} | user={t.user_id} | amount={t.amount} | risk={t.risk_score}")


def _show_flagged(detector):
    flagged = detector.get_flagged()
    if not flagged:
        print("\nNo flagged transactions.")
        return

    ranked = merge_sort(flagged, key=lambda t: t.risk_score, reverse=True)

    print(f"\n{len(ranked)} flagged transaction(s), ranked by risk:")
    for t in ranked:
        print(f"  {t.txn_id} | user={t.user_id} | amount={t.amount} | "
              f"risk={t.risk_score} | flags={t.flags}")


def _show_top_k(detector):
    flagged = detector.get_flagged()
    if not flagged:
        print("\nNo flagged transactions to rank.")
        return

    try:
        k = int(input("How many top risky transactions to show? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    risk_heap = RiskHeap()
    for t in flagged:
        risk_heap.push(t)

    print(f"\nTop {k} riskiest transactions:")
    for t in risk_heap.top_k(k):
        print(f"  {t.txn_id} | user={t.user_id} | risk={t.risk_score} | flags={t.flags}")


def _show_fraud_rings(detector):
    rings = detector.get_fraud_rings()
    if not rings:
        print("\nNo suspicious device-sharing clusters found.")
        return

    print(f"\n{len(rings)} suspicious cluster(s) found:")
    for i, cluster in enumerate(rings, start=1):
        print(f"  Cluster {i}: {cluster}")


def _search_by_range(detector):
    try:
        low = float(input("Enter minimum amount: "))
        high = float(input("Enter maximum amount: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    results = detector.amount_tree.range_query(low, high)
    if not results:
        print(f"\nNo transactions found between {low} and {high}.")
        return

    print(f"\n{len(results)} transaction(s) between {low} and {high}:")
    for t in results:
        print(f"  {t.txn_id} | user={t.user_id} | amount={t.amount}")