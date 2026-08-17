import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Endpoints {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String baseUrl = "https://api.example.com/v1";

        getResource(client, baseUrl + "/users");
        createResource(client, baseUrl + "/users");
        updateResource(client, baseUrl + "/users/42");
        deleteResource(client, baseUrl + "/users/42");
    }

    private static void getResource(HttpClient client, String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
        System.out.println("GET " + client.send(request, HttpResponse.BodyHandlers.ofString()).body());
    }

    private static void createResource(HttpClient client, String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString("{\"name\":\"Alice\"}"))
                .build();
        System.out.println("POST " + client.send(request, HttpResponse.BodyHandlers.ofString()).body());
    }

    private static void updateResource(HttpClient client, String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .PUT(HttpRequest.BodyPublishers.ofString("{\"name\":\"Alice Updated\"}"))
                .build();
        System.out.println("PUT " + client.send(request, HttpResponse.BodyHandlers.ofString()).body());
    }

    private static void deleteResource(HttpClient client, String url) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .DELETE()
                .build();
        System.out.println("DELETE " + client.send(request, HttpResponse.BodyHandlers.ofString()).statusCode());
    }
}