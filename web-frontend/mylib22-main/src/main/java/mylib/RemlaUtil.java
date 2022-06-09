package mylib;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.charset.StandardCharsets;

public class RemlaUtil {

	public static String getHostName() {
		try {
			return InetAddress.getLocalHost().getHostName();
		} catch (UnknownHostException e) {
			return "Unknown";
		}
	}

	public static String getUtilVersion() {
		try (InputStream is = RemlaUtil.class.getClassLoader().getResourceAsStream("version.txt");
				InputStreamReader isr = new InputStreamReader(is, StandardCharsets.UTF_8);
				BufferedReader br = new BufferedReader(isr)) {

			return br.readLine().trim();

		} catch (IOException e) {
			return "<io error>";
		}
	}
}