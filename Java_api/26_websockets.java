import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.WebSocket;
import java.net.http.WebSocket.Listener;
import java.util.concurrent.CompletionStage;

public class Websockets {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        WebSocket socket = client.newWebSocketBuilder()
                .buildAsync(URI.create("wss://stream.example.com/ws"),
                        new Listener() {
                            @Override
                            public void onOpen(WebSocket webSocket) {
                                System.out.println("Connected to WebSocket");
                                webSocket.sendText("{\"subscribe\":\"market.data\"}", true);
                                webSocket.request(1);
                            }

                            @Override
                            public CompletionStage<?> onText(WebSocket webSocket, CharSequence data, boolean last) {
                                System.out.println("Message: " + data);
                                webSocket.request(1);
                                return null;
                            }

                            @Override
                            public CompletionStage<?> onClose(WebSocket webSocket, int statusCode, String reason) {
                                System.out.println("Closed: " + statusCode + " " + reason);
                                return null;
                            }
                        })
                .get();

        Thread.sleep(10_000);
        socket.sendClose(WebSocket.NORMAL_CLOSURE, "done");
    }
}