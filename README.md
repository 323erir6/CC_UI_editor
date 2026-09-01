# CC:Tweaked UI Editor

Visual editor for CC:Tweaked computer and monitor interfaces. The application has a redesigned dark UI and supports English and Russian; English is selected by default.

## Запуск

Відкрийте `cc_terminal_ui_editor.pyw` подвійним кліком або запустіть:

```powershell
pythonw cc_terminal_ui_editor.pyw
```

The default canvas matches an Advanced Computer terminal: `51 × 19` characters. Use **New** to enter a different monitor size. The `EN / RU` switch in the upper-right corner changes the interface language immediately.

## Робота

- виберіть інструмент, символ, колір тексту та фону;
- малюйте пензлем, текстом, прямокутником або заливкою;
- **Solid cell** повністю зафарбовує клітинку вибраним фоновим кольором, записуючи в неї пробіл;
- доступні лінії, заповнені та контурні прямокутники й еліпси;
- інструмент **Select** підтримує копіювання, вирізання, вставлення та видалення області;
- гарячі клавіші виділення: `Ctrl+C`, `Ctrl+X`, `Ctrl+V`, `Delete`;
- кольори тексту та фону можна швидко поміняти місцями;
- права кнопка на кольорі швидко вибирає його як колір тексту;
- **Копіювати Lua** кладе готову програму в буфер обміну;
- Lua-код у правій панелі можна редагувати: підтримувані зміни автоматично застосовуються назад до полотна;
- кнопка **Apply code** застосовує код одразу, без очікування автоматичного оновлення;
- вставте код у редактор CC:Tweaked і запустіть його;
- проєкт можна зберегти у файл `.ccui.json`, а готовий код — експортувати у `.lua`.

Генератор не створює окрему команду для кожної клітинки. Він будує два варіанти програми та залишає коротший: рядки через `term.blit()` або суцільні області через `paintutils.drawFilledBox()`. Повторювані посилання на функції також скорочуються локальними псевдонімами. Завдяки цьому великі панелі, фони й прямокутники зазвичай займають лише одну команду Lua.

Зворотний перегляд розуміє `setBackgroundColor`, `setTextColor`, `clear`, `clearLine`, `setCursorPos`, `write`, `blit`, а також `paintutils.drawPixel`, `drawLine`, `drawBox` і `drawFilledBox`. Інший Lua-код не виконується на комп'ютері й безпечно ігнорується.
