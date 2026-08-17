import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Base64;

public class OAuth2 {

    private static final String CLIENT_ID = System.getenv("CLIENT_ID");
    private static final String CLIENT_SECRET = System.getenv("CLIENT_SECRET");

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String credentials = Base64.getEncoder()
                .encodeToString((CLIENT_ID + ":" + CLIENT_SECRET).getBytes());

        String form = "grant_type=client_credentials&scope=read:data";

        HttpRequest tokenRequest = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/oauth/token"))
                .header("Authorization", "Basic " + credentials)
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString(form))
                .build();

        HttpResponse<String> tokenResponse = client.send(tokenRequest, HttpResponse.BodyHandlers.ofString());

        System.out.println("Token response: " + tokenResponse.body());
    }
}