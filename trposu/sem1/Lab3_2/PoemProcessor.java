import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

public class PoemProcessor {

    public static void main(String[] args) throws Exception {
        String encKey = "1234567890123456";
        String originalString = readFile("lab3text_vanya/input.txt");

        int vowelWordCount = countVowelWords(originalString);

        String encryptedString = encrypt(originalString, encKey);
        writeToFile("lab3text_vanya", "output.txt", encryptedString);

        System.out.println("File contents: " + originalString);
        System.out.println("Number of words that begin and end with a vowel: " + vowelWordCount);
        System.out.println("Encrypted string: " + encryptedString);
        System.out.println("Decrypted string: " + decrypt(encryptedString, encKey));
    }

    private static String readFile(String filePath) {
        try {
            byte[] bytes = Files.readAllBytes(Paths.get(filePath));
            return new String(bytes, StandardCharsets.UTF_8);
        } catch (IOException e) {
            e.printStackTrace();
            return "The input file is empty";
        }
    }

    private static void writeToFile(String directoryPath, String fileName, String content) {
        File directory = new File(directoryPath);
        if (!directory.exists()) {
            directory.mkdirs();
        }
        File file = new File(directory, fileName);
        try {
            Files.write(file.toPath(), content.getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static int countVowelWords(String str) {
        int count = 0;
        String[] words = str.split("\\s+");
        for (String word : words) {
            if (word.matches("^[ауоыиэяюёеАУОЫИЭЯЮЁЕ].*[ауоыиэяюёеАУОЫИЭЯЮЁЕ]$")) {  // регулярное выражение
                count++;
            }
        }
        return count;
    }

    public static String encrypt(String input, String key) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        byte[] encryptedBytes = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    public static String decrypt(String input, String key) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, keySpec);
        byte[] encryptedBytes = Base64.getDecoder().decode(input);
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }
}
