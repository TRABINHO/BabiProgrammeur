"""Probe : comment Kivy 2.3 calcule-t-il minimum_height (padding ? spacing ?)."""
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

b = BoxLayout(padding=14, spacing=12, size_hint_y=None, width=100, height=0)
w1 = Widget(size_hint_y=None, height=100)
w2 = Widget(size_hint_y=None, height=50)
b.add_widget(w1)
b.add_widget(w2)
b.do_layout()
print("hauteurs enfants :", [c.height for c in b.children])
print("padding          :", b.padding, "| spacing :", b.spacing)
print("minimum_height 1 :", b.minimum_height)
# forcer la recalcul complet (AliasProperty mis en cache trop tôt)
for _ in range(3):
    Clock.tick()
print("minimum_height 2 :", b.minimum_height, "<- après ticks")
print("somme directe    :", 100 + 50 + 12 + 28, "(50+100+spacing+padding*2)")
