import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class RateLimits {

    private static final int MAX_REQUESTS = 100;

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        int requestsMade = 0;

        while (requestsMade < MAX_REQUESTS) {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.example.com/v1/fetch?page=1"))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            String remaining = response.headers().firstValue("X-RateLimit-Remaining").orElse("unknown");
            String reset = response.headers().firstValue("X-RateLimit-Reset").orElse("unknown");

            System.out.printf("Request %d | Remaining: %s | Reset at: %s%n",
                    requestsMade + 1, remaining, reset);

            if (response.statusCode() == 429) {
                long retryAfter = Long.parseLong(
                        response.headers().firstValue("Retry-After").orElse("60"));
                System.out.println("Rate limited, waiting " + retryAfter + " seconds...");
                Thread.sleep(retryAfter * 1000L);
                continue;
            }

            requestsMade++;
        }
    }
}