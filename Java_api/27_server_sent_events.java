import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ServerSentEvents {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/events/stream"))
                .header("Accept", "text/event-stream")
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        String[] lines = response.body().split("\\n");
        for (String line : lines) {
            if (line.startsWith("data:")) {
                String event = line.substring(5).trim();
                System.out.println("Event received: " + event);
            }
        }
    }
}