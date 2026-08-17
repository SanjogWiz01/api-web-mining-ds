import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ErrorHandling {

    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();

        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.example.com/v1/missing"))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            switch (response.statusCode()) {
                case 200 -> System.out.println("Success: " + response.body());
                case 400 -> System.err.println("Bad request - check parameters");
                case 401 -> System.err.println("Unauthorized - check credentials");
                case 403 -> System.err.println("Forbidden - insufficient permissions");
                case 404 -> System.err.println("Not found - resource missing");
                case 429 -> System.err.println("Rate limited - slow down");
                case 500 -> System.err.println("Server error - retry later");
                default -> System.err.println("Unexpected status: " + response.statusCode());
            }
        } catch (Exception e) {
            System.err.println("Request failed: " + e.getMessage());
        }
    }
}