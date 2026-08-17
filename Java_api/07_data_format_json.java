import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

public class DataFormatJson {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String jsonBody = """
                {
                  "name": "Alice",
                  "age": 30,
                  "tags": ["java", "api", "json"],
                  "active": true,
                  "address": {
                    "city": "Kathmandu",
                    "country": "Nepal"
                  }
                }
                """;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/users"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        Map<String, String> contentType = response.headers().map();
        System.out.println("Content-Type: " + contentType.getOrDefault("content-type", "unknown"));
        System.out.println("Created user response: " + response.body());
    }
}