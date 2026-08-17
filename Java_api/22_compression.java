import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.zip.GZIPInputStream;
import java.io.ByteArrayInputStream;

public class Compression {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/big-dataset"))
                .header("Accept-Encoding", "gzip, deflate")
                .GET()
                .build();

        HttpResponse<byte[]> response = client.send(request, HttpResponse.BodyHandlers.ofByteArray());

        String encoding = response.headers().firstValue("Content-Encoding").orElse("none");
        System.out.println("Content-Encoding: " + encoding);
        System.out.println("Received bytes: " + response.body().length);

        if (encoding.equalsIgnoreCase("gzip")) {
            GZIPInputStream gzip = new GZIPInputStream(new ByteArrayInputStream(response.body()));
            String decompressed = new String(gzip.readAllBytes());
            System.out.println("Decompressed body (first 100 chars): " + decompressed.substring(0, 100));
        }
    }
}