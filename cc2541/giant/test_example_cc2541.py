import example_cc2541
import subprocess


def disable_crp():
    output = subprocess.check_output(
        ["cc-tool", "--erase", "--log"],
        stderr=subprocess.STDOUT
    )
    return output


def enable_crp():
    output = subprocess.check_output(
        ["cc-tool", "--lock", "debug", "--log"],
        stderr=subprocess.STDOUT
    )
    return output


def test_check_protected():
    # No CRP
    disable_crp()
    protected = example_cc2541.check_protected()
    assert protected == False

    # With CRP
    enable_crp()
    protected = example_cc2541.check_protected()
    assert protected == True

    # Exception
    protected = example_cc2541.check_protected()
    assert protected == None


def main():
    test_check_protected()


if __name__ == "__main__":
    main()
