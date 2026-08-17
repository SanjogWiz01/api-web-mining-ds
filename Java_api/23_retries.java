import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Retries {

    private static final int MAX_RETRIES = 3;

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        int attempt = 0;
        boolean success = false;

        while (attempt < MAX_RETRIES && !success) {
            attempt++;
            try {
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create("https://api.example.com/v1/fragile"))
                        .GET()
                        .build();

                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

                if (response.statusCode() == 200) {
                    System.out.println("Success on attempt " + attempt);
                    success = true;
                } else {
                    System.out.println("Attempt " + attempt + " -> status " + response.statusCode());
                    if (response.statusCode() >= 500) {
                        Thread.sleep(1000L * attempt);
                    } else {
                        break;
                    }
                }
            } catch (Exception e) {
                System.out.println("Attempt " + attempt + " -> error: " + e.getMessage());
                Thread.sleep(1000L * attempt);
            }
        }

        if (!success) {
            System.err.println("Request failed after " + MAX_RETRIES + " attempts");
        }
    }
}