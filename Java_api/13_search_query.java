import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;

public class SearchQuery {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String searchTerm = "java api web mining";
        String encoded = URLEncoder.encode(searchTerm, StandardCharsets.UTF_8);

        String url = "https://api.example.com/v1/search?q=" + encoded
                + "&language=en&num=10&safe=active";

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println("Search for: " + searchTerm);
        System.out.println("Encoded URL: " + url);
        System.out.println("Results: " + response.body());
    }
}