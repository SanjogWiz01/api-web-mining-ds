import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Webhooks {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String payload = """
                {
                  "event": "data.updated",
                  "resource_id": "abc-123",
                  "timestamp": "2026-08-17T10:00:00Z"
                }
                """;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://your-server.example.com/webhook"))
                .header("Content-Type", "application/json")
                .header("X-Signature", "sha256=computedsignaturehere")
                .POST(HttpRequest.BodyPublishers.ofString(payload))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() == 200 || response.statusCode() == 204) {
            System.out.println("Webhook delivered successfully");
        } else {
            System.err.println("Webhook delivery failed: " + response.statusCode());
        }
    }
}