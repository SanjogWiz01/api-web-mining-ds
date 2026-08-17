import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ApiVersioning {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        requestV1(client);
        requestV2(client);
    }

    private static void requestV1(HttpClient client) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/items"))
                .header("Accept", "application/vnd.example.v1+json")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("v1 -> " + response.statusCode() + " " + response.body());
    }

    private static void requestV2(HttpClient client) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v2/items"))
                .header("Accept", "application/vnd.example.v2+json")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("v2 -> " + response.statusCode() + " " + response.body());
    }
}