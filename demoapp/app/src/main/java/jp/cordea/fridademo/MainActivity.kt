package jp.cordea.fridademo

import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import jp.cordea.fridademo.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private val detector = Detector()
    private var count = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.toolbar)

        binding.fab.setOnClickListener {
            ++count
            binding.content.textView.text = count.toString()
        }
        binding.content.textView.text = count.toString()

        binding.content.button.setOnClickListener {
            if (detector.detect()) {
                Toast.makeText(this, "DO NOT SHOW THIS TOAST!!", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}
