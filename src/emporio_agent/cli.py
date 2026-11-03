# Simple chat in the terminal

from emporio_agent.agent import Agent

HELP = "Comandos: /reset (nova conversa), /tools (mostrar/esconder tools usadas), /sair (sair)"


def main():
    try:
        agent = Agent()
    except RuntimeError as error:
        print(error)
        return
    show_tools = True

    print("=== Empório da Música - Atendimento ===")
    print(HELP)
    print()

    while True:
        try:
            message = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if message == "":
            continue
        if message in ["/sair", "/exit", "/quit"]:
            break
        if message == "/reset":
            agent.reset()
            print("(conversa reiniciada)\n")
            continue
        if message == "/tools":
            show_tools = not show_tools
            print("(tools visíveis)\n" if show_tools else "(tools escondidas)\n")
            continue

        try:
            answer, tool_calls = agent.send(message)
        except Exception as error:
            # Network or API errors (like rate limit) should not close the chat
            print(f"[erro] {error}\n")
            continue

        if show_tools:
            for call in tool_calls:
                print(f"  [tool] {call}")
        print(f"Empório: {answer}\n")

    print("Até mais! 🎸")


if __name__ == "__main__":
    main()
