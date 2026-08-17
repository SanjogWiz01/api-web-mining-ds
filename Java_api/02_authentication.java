import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Authentication {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/account"))
                .header("Authorization", "Bearer YOUR_ACCESS_TOKEN")
                .header("X-Api-Key", "YOUR_API_KEY")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() == 401) {
            System.out.println("Authentication failed - token expired or invalid");
        } else if (response.statusCode() == 200) {
            System.out.println("Authenticated successfully");
        }
    }
}