Logic magnet 
قمت بإنشاء board من خلال تعريف كلاس game board


GameBoard مسؤول عن إدارة الحالة الحالية للعبة وتنفيذ العمليات المرتبطة بتحريك العناصر وتحديث الشبكة
بداخله تابع init وظيفته هو تهيئة حالة اللعبة عند إنشاء كائن جديد من هذا الكلاس. يتم ذلك عن طريق إعداد الشبكة، أبعادها، وحالتها الحالية بداخله بارميتر  grid_layout (وهي مصفوفة ثنائية الأبعاد تمثل الشبكة
طبعا الشبكة هي عبارة عن list من خلايا  هذه الخلايا ممكن ان تكون كرات حديدية او اهداف او مغناطيس او none.


الحالة الابتدائية (Initial State):
يتم تمثيل الحالة البدائية بواسطة شبكة grid، وهي عبارة عن مصفوفة ثنائية الأبعاد تتكون من كائنات من نوع Cell.
كل خلية (Cell) في الشبكة يمكن أن تحتوي على:
عنصر (Item) بلون معين: (مثل "red"، "blue"، أو "gray").
هدف (Goal): خلايا معينة تستهدف احتواء عنصر ما.
تكون الخلايا الفارغة دون عناصر أو أهداف.
يتم تحديد الشبكة في وقت إنشاء الكائن بواسطة grid_layout، وهي معطى يتم تمريره إلى الكلاس.

. فضاء الحالات (State Space)
فضاء الحالات هو جميع التوزيعات الممكنة للعناصر داخل الشبكة grid.
يتغير فضاء الحالة عند:
تحريك عنصر يدويًا.
تحديث موقع العناصر الرمادية استجابةً لتحريك العناصر الحمراء أو الزرقاء.
تعريف حالة معينة:
تمثل الحالة بواسطة المواقع الحالية للعناصر في الشبكة، والمعلومات المتعلقة بالخلايا التي تحتوي على أهداف (goal) وما إذا كانت محققة.
قيود الحركة:
لا يمكن نقل عنصر إلى خلية غير فارغة.
لا يمكن تحريك العناصر الرمادية يدويًا.
الانتقالات الممكنة:
يتم تحديد التحركات بناءً على اتجاهات محددة (أعلى، أسفل، يمين، يسار).
لكل عنصر، يمكن تنفيذه باستخدام:
swap_item(x1, y1, item, new_x, new_y): لحركة مباشرة للعناصر.
swap_auto_item(x1, y1, item, new_x, new_y): لتحريك العناصر الرمادية تلقائيًا استجابة لتحريك الأحمر أو الأزرق.





class and function:
قمت  بانشاء عدة كلاسات منها
Class Item
Attributes:
hue:
نوع العنصر أو لونه (مثل "gray" أو "red" أو "blue"). يحدد سلوك العنصر على اللوحة.
position:
الموقع الحالي للعنصر في الشبكة على هيئة إحداثيات (x, y).
Methods:
init(self, hue):
ينشئ كائن عنصر جديد بلون معين، ويترك موضعه فارغًا عند الإنشاء.
str(self):
يُعيد حرفًا أوليًا يمثل العنصر بناءً على لونه (على سبيل المثال، 'R' إذا كان لونه 'red').
Class Cell
Attributes:
item:
العنصر الموجود في الخلية (إن وجد). يكون إما كائنًا من نوع Item أو None إذا كانت الخلية فارغة.
target:
إذا كانت الخلية هدفًا، يتم تعيين القيمة إلى "goal"؛ وإلا تكون القيمة None.
position:
موقع الخلية في الشبكة (غير مستخدم بشكل مباشر هنا).
Methods:
init(self, item, target):

ينشئ خلية تحتوي على عنصر معين أو هدف (goal) أو تكون فارغة.
str(self):

يُعيد الحرف "G" إذا كانت الخلية هدفًا (goal)، وإلا لا يُعيد شيئًا.
Class GameBoard
Attributes:
grid:
تمثل الشبكة الكاملة للعبة، وهي عبارة عن قائمة من القوائم تحتوي على كائنات Cell.
size:
عدد الصفوف في الشبكة.
num_cols:
عدد الأعمدة في الشبكة.
Methods:
init(self, grid_layout):

تهيئ الشبكة باستخدام تخطيط معين (grid_layout).
swap_item(self, x1, y1, item, new_x, new_y):

تنقل عنصرًا معينًا (item) من موقعه الحالي (x1, y1) إلى موقع جديد (new_x, new_y).
تتحقق من قواعد اللعبة الخاصة بالعناصر (مثل تأثير اللون الأحمر أو الأزرق على العناصر الرمادية).
swap_auto_item(self, x1, y1, item, new_x, new_y):

عملية نقل تلقائي للعناصر، تُستخدم كجزء من المنطق في swap_item.
is_completed(self):

يتحقق مما إذا كانت اللعبة مكتملة، أي إذا كان كل هدف (goal) يحتوي على عنصر.
Class MagneticGameSolver
Attributes:
game_board:
اللوحة الحالية للعبة التي سيتم حلها.
Methods:
init(self, game_board):

تهيئ كائن الحل باستخدام اللوحة التي سيتم التعامل معها.
bfs(self):

يحاول حل اللعبة باستخدام خوارزمية البحث بعرض (Breadth-First Search).
يبدأ من مواقع العناصر الحمراء والزرقاء، ويتحقق من كل حركة ممكنة.
إذا نجح في إكمال اللعبة، يُعيد True؛ وإلا يُعيد False.


البحث التلقائي (BFS):
طبعا bfs يعمل من خلال مبدا FIFO(firs in first out)
اي العنصر الذي يدخل اولا هو العنصر الذي يعالج اولا 

يستخدم MagneticGameSolver.bfs() لحل اللعبة تلقائيًا.
يتم استكشاف فضاء الحالات باستخدام خوارزمية بحث عن أقصر مسار (BFS)، ويقوم بتوليد الحالات حتى الوصول إلى الحل.
الاستراتيجية التلقائية (BFS):
هدف BFS:
إيجاد تسلسل حركات يؤدي إلى تحقيق الحالة النهائية.
الخطوات:
البدء بالحالة الأولية.
استكشاف جميع التحركات الممكنة من الحالة الحالية.


الحالة النهائية:Final State
هي حالة الفوز اي عندما تكون جميع الاهداف بداخلها كرات حديدية او مغناطيس

التحقق بعد كل حركة ما إذا كانت الحالة النهائية قد تحققت.
إذا لم تتحقق الحالة النهائية، يتم إضافة الحالات الجديدة إلى الطابور لمزيد من الاستكشاف.
إذا تم استنفاد جميع الحالات ولم يتم الوصول إلى الحل، يتم الإبلاغ بعدم إمكانية الحل.
