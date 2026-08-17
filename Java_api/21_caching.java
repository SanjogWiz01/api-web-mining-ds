import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.LinkedHashMap;
import java.util.Map;

public class Caching {

    private static final Map<String, String> CACHE = new LinkedHashMap<>();

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String url = "https://api.example.com/v1/popular";

        String cached = CACHE.get(url);
        if (cached != null) {
            System.out.println("Serving from cache (no API call)");
            System.out.println(cached);
            return;
        }

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Cache-Control", "max-age=3600")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() == 200) {
            CACHE.put(url, response.body());
            System.out.println("Cached new response");
        }

        System.out.println("API response: " + response.body());
    }
}