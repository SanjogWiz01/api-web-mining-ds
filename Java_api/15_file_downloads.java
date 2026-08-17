import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;

public class FileDownloads {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/export.csv"))
                .GET()
                .build();

        HttpResponse<byte[]> response = client.send(request, HttpResponse.BodyHandlers.ofByteArray());

        if (response.statusCode() == 200) {
            Path output = Path.of("download.csv");
            Files.write(output, response.body());
            System.out.println("Downloaded " + response.body().length + " bytes to " + output.toAbsolutePath());
        } else {
            System.err.println("Download failed with status " + response.statusCode());
        }
    }
}