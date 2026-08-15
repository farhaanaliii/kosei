package {package_name};

import android.app.Application;
import android.content.Intent;

import java.io.PrintWriter;
import java.io.StringWriter;

public class Applications extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        
        final Thread.UncaughtExceptionHandler defaultHandler = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
            @Override
            public void uncaughtException(Thread thread, Throwable ex) {
                Intent intent = new Intent(getApplicationContext(), CrashActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                intent.putExtra("error", getStackTrace(ex));
                startActivity(intent);
                
                if (defaultHandler != null) {
                    defaultHandler.uncaughtException(thread, ex);
                } else {
                    System.exit(2);
                }
            }
        });
    }

    private String getStackTrace(Throwable th) {
        StringWriter result = new StringWriter();
        th.printStackTrace(new PrintWriter(result));
        return result.toString();
    }
}
