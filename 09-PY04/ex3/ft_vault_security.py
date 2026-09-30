#!/usr/bin/env python3


def secure_archive(
    filename: str, mode: str = "read", content: str = ""
) -> tuple[bool, str]:
    if mode == "read":
        try:
            with open(filename, "r") as f:
                data = f.read()
            return (True, data)
        except Exception as e:
            return (False, str(e))
    elif mode == "write":
        try:
            with open(filename, "w") as f:
                f.write(content)
            return (True, "Content successfully written to file")
        except Exception as e:
            return (False, str(e))
    else:
        return (False, "Invalid mode operation")


def main() -> None:
    print("=== Cyber Archives Security ===")
    secure_archive(
        "ancient_fragment.txt",
        mode="write",
        content="... Cyber Archives Data ...\n",
    )

    print("Using 'secure_archive' to read from a nonexistent file:")
    res1 = secure_archive("/not/existing/file", mode="read")
    print(f"({res1[0]}, \"{res1[1]}\")")

    print("Using 'secure_archive' to read from an inaccessible file:")
    res2 = secure_archive("/etc/master.passwd", mode="read")
    print(f"({res2[0]}, \"{res2[1]}\")")

    print("Using 'secure_archive' to read from a regular file:")
    res3 = secure_archive("ancient_fragment.txt", mode="read")
    raw_str = repr(res3[1])
    print(f"({res3[0]}, {raw_str})")

    print("Using 'secure_archive' to write previous content to a new file:")
    if res3[0]:
        res4 = secure_archive(
            "secured_fragment.txt", mode="write", content=res3[1]
        )
        print(f"({res4[0]}, '{res4[1]}')")


if __name__ == "__main__":
    main()
