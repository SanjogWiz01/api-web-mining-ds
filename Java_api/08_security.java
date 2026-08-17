import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Security {

    private static final String API_KEY = System.getenv("API_KEY");

    public static void main(String[] args) throws Exception {
        if (API_KEY == null || API_KEY.isBlank()) {
            System.err.println("API_KEY environment variable is not set");
            return;
        }

        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/secure/data"))
                .header("X-Api-Key", API_KEY)
                .header("X-Request-Signature", generateSignature(API_KEY))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.statusCode() + " -> " + response.body());
    }

    private static String generateSignature(String key) {
        return Integer.toHexString(key.hashCode());
    }
}