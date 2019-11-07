package MKAgentRef;

import MKAgent.InvalidMessageException;
import java.io.BufferedReader;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;

public class Main {
	private static final int holes = 7;
	private static final int seeds = 7;
	private static Reader input;

	static {
		input = new BufferedReader(new InputStreamReader(System.in));
	}

	public static void sendMsg(String msg) {
		System.out.print(msg);
		System.out.flush();
	}

	public static String recvMsg() throws IOException {
		StringBuilder message = new StringBuilder();

		int newCharacter;
		do {
			newCharacter = input.read();
			if (newCharacter == -1) {
				throw new EOFException("Input ended unexpectedly.");
			}

			message.append((char)newCharacter);
		} while((char)newCharacter != '\n');

		return message.toString();
	}

	public static void main(String[] args) {
		try {
			(new Agent(7, 7)).play();
		} catch (IOException var2) {
			System.err.println("Communication error: " + var2.getMessage());
		} catch (InvalidMessageException var3) {
			System.err.println("THIS IS A REAL BUG: " + var3.getMessage());
		}

	}
}