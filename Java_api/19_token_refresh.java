import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class TokenRefresh {

    private static String accessToken = System.getenv("ACCESS_TOKEN");
    private static final String REFRESH_TOKEN = System.getenv("REFRESH_TOKEN");

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        HttpResponse<String> response = callApi(client);

        if (response.statusCode() == 401) {
            System.out.println("Access token expired, refreshing...");
            accessToken = refreshAccessToken(client);
            response = callApi(client);
        }

        System.out.println("Final response: " + response.statusCode() + " -> " + response.body());
    }

    private static HttpResponse<String> callApi(HttpClient client) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/data"))
                .header("Authorization", "Bearer " + accessToken)
                .GET()
                .build();
        return client.send(request, HttpResponse.BodyHandlers.ofString());
    }

    private static String refreshAccessToken(HttpClient client) throws Exception {
        String form = "grant_type=refresh_token&refresh_token=" + REFRESH_TOKEN;
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/oauth/token"))
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString(form))
                .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Refresh response: " + response.body());
        return "NEW_ACCESS_TOKEN_FROM_RESPONSE";
    }
}