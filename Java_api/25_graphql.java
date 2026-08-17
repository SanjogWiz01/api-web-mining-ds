import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Graphql {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String query = """
                {
                  "query": "query { user(id: 1) { id name posts { title } } }",
                  "variables": {}
                }
                """;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/graphql"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer YOUR_TOKEN")
                .POST(HttpRequest.BodyPublishers.ofString(query))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println("GraphQL status: " + response.statusCode());
        System.out.println("Response: " + response.body());
    }
}