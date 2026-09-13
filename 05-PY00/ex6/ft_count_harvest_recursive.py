def ft_count_harvest_recursive() -> None:

    def count_days(count: int) -> None:
        if count < harvest:
            print(f"Day {count + 1}")
            count_days(count + 1)

    harvest = int(input("Days until harvest: "))
    count_days(0)
    print("Harvest time!")
