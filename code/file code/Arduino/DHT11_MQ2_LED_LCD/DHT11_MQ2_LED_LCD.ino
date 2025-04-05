#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 16       // Chân G16 nối với DHT11
#define DHTTYPE DHT11   // Định nghĩa loại cảm biến là DHT11
#define LED_PIN 2       // Chân G2 nối với LED
#define MQ2_PIN 32      // Chân G32 nối với MQ2

// Khởi tạo cảm biến DHT
DHT dht(DHTPIN, DHTTYPE);

// Khởi tạo LCD với địa chỉ I2C là 0x27
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(LED_PIN, OUTPUT);
  pinMode(MQ2_PIN, INPUT);

  // Khởi tạo LCD
  lcd.init();
  lcd.backlight();

  // In tiêu đề dữ liệu lên Plotter (tùy chọn)
  Serial.println("Nhiệt độ\tNồng độ khói");
}

void loop() {
  // Đọc giá trị nhiệt độ từ DHT11
  float temperature = dht.readTemperature();
  int mq2Value = analogRead(MQ2_PIN);

  // Kiểm tra lỗi khi đọc cảm biến DHT11
  if (isnan(temperature)) {
    Serial.println("Lỗi đọc dữ liệu từ cảm biến DHT11!");
    lcd.setCursor(0, 0);
    lcd.print("DHT11 Error     ");
  } else {
    // Hiển thị nhiệt độ lên Serial và LCD
    Serial.print("Nhiệt độ: ");
    Serial.print(temperature);
    Serial.println("°C");

    lcd.setCursor(0, 0);
    lcd.print("Nhiet do: ");
    lcd.print(temperature);
    lcd.print(" C   ");
  }

  // Đọc và hiển thị giá trị nồng độ khói từ MQ2
  Serial.print("Nồng độ khói (MQ2): ");
  Serial.println(mq2Value);

  lcd.setCursor(0, 1);
  lcd.print("Khoi: ");
  lcd.print(mq2Value);
  lcd.print("     ");

  // Điều khiển LED theo nhiệt độ
  if (temperature > 30) {
    digitalWrite(LED_PIN, HIGH);  // Bật LED nếu nhiệt độ trên 30°C
  } else {
    digitalWrite(LED_PIN, LOW);   // Tắt LED nếu nhiệt độ dưới 30°C
  }

  // Gửi dữ liệu lên Plotter (nhiệt độ và nồng độ khói)
  Serial.print(temperature);
  Serial.print("\t"); // Dấu tab để phân biệt giá trị
  Serial.println(mq2Value);

  delay(1000);  // Đợi 1 giây trước khi cập nhật lại
}
