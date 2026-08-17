import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class RateLimitHeaders {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        for (int i = 0; i < 5; i++) {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.example.com/v1/resource"))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            String limit = response.headers().firstValue("X-RateLimit-Limit").orElse("?");
            String remaining = response.headers().firstValue("X-RateLimit-Remaining").orElse("?");
            String reset = response.headers().firstValue("X-RateLimit-Reset").orElse("?");

            System.out.printf("Request %d | Limit: %s | Remaining: %s | Reset: %s%n",
                    i + 1, limit, remaining, reset);
        }
    }
}