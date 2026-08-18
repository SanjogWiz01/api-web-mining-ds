import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.time.Instant;

public class ApiMonitoring {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        for (int i = 0; i < 10; i++) {
            Instant start = Instant.now();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.example.com/v1/health"))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            Duration elapsed = Duration.between(start, Instant.now());

            boolean healthy = response.statusCode() == 200 && elapsed.toMillis() < 1000;
            System.out.printf("Check %d | status=%d | latency=%dms | %s%n",
                    i + 1, response.statusCode(), elapsed.toMillis(),
                    healthy ? "HEALTHY" : "UNHEALTHY");
        }
    }
}