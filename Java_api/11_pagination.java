import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Pagination {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        String baseUrl = "https://api.example.com/v1/items";

        int page = 1;
        boolean hasMore = true;

        while (hasMore) {
            String url = baseUrl + "?page=" + page + "&limit=25";
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("Page " + page + " -> " + response.body());

            String nextLink = response.headers()
                    .firstValue("Link")
                    .orElse("")
                    .contains("rel=\"next\"") ? "yes" : "no";

            if (nextLink.equals("no") || page >= 10) {
                hasMore = false;
            } else {
                page++;
            }
        }

        System.out.println("Fetched " + (page) + " pages total.");
    }
}