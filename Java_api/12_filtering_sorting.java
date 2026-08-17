import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class FilteringSorting {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String query = Stream.of(
                "status=active",
                "type=article",
                "created_after=2024-01-01",
                "created_before=2024-12-31",
                "sort=-created_at",
                "fields=id,title,url"
        ).collect(Collectors.joining("&"));

        String url = "https://api.example.com/v1/items?" + query;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println("Request URL: " + url);
        System.out.println("Filtered & sorted results: " + response.body());
    }
}