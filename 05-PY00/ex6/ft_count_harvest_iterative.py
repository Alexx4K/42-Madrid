def ft_count_harvest_iterative() -> None:

    count: int = 0
    harvest = int(input("Days until harvest: "))
    for i in range(harvest):
        count += 1
        print(f"Day {count}")
    print("Harvest time!")
