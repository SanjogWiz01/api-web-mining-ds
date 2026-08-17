import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

public class BatchRequests {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        List<String> ids = List.of("1001", "1002", "1003", "1004", "1005");
        List<HttpResponse<String>> responses = new ArrayList<>();

        for (String id : ids) {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.example.com/v1/items/" + id))
                    .GET()
                    .build();
            responses.add(client.send(request, HttpResponse.BodyHandlers.ofString()));
        }

        int success = 0;
        for (HttpResponse<String> response : responses) {
            if (response.statusCode() == 200) success++;
        }

        System.out.println("Batch completed: " + success + "/" + ids.size() + " succeeded");
    }
}