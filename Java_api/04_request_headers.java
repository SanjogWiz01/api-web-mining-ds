import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class RequestHeaders {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/resource"))
                .header("Accept", "application/json")
                .header("Accept-Language", "en-US,en;q=0.9")
                .header("User-Agent", "java-api-client/1.0")
                .header("X-Request-Id", java.util.UUID.randomUUID().toString())
                .header("Content-Type", "application/json; charset=UTF-8")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        String rateLimit = response.headers().firstValue("X-RateLimit-Remaining").orElse("n/a");
        System.out.println("Remaining rate limit: " + rateLimit);
        System.out.println("Response: " + response.body());
    }
}