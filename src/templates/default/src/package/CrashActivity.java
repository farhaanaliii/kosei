package {package_name};

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;

public class CrashActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        String tempErrMsg = "Unknown error";
        Intent intent = getIntent();
        if (intent != null && intent.hasExtra("error")) {
            tempErrMsg = intent.getStringExtra("error");
        }
        final String errMsg = tempErrMsg;
        
        AlertDialog.Builder bld = new AlertDialog.Builder(this);
        bld.setTitle("An error occurred");
        bld.setMessage(errMsg);
        bld.setCancelable(false);
        bld.setPositiveButton("Copy", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                ClipData clip = ClipData.newPlainText("Error Log", errMsg);
                if (clipboard != null) {
                    clipboard.setPrimaryClip(clip);
                    Toast.makeText(CrashActivity.this, "Copied to clipboard", Toast.LENGTH_SHORT).show();
                }
                finish();
            }
        });
        bld.setNegativeButton("End Application", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                finish();
            }
        });
        bld.create().show();
    }
}