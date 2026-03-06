# Changelog

_Created On 6th March 2026._

**6th March 2026**

1) updated gitignore for PyCharm and probably ever JetBrains IDE ever, which I am ABSOLUTELY LOVING.
2) *sigh...* Readded Utilities folder to the repo. Also realized it is VERY inconvienent to have files temp files you
   don't want to untrack AND normal project files in the same tracked folder.
3) updated readme?? with what I don't even know and remember I'm creating the changelog up to this date by looking at my
   lazy ass 5 word commit messages and IDFK. Need proper change messages...
4) **ADDED A CHANGELOG.MD !! YAYYY!!!**
5) updated readme for card_engine (god I love that project)

expanding on no.2, the utilities folder:

I made a csv reader and a function to search for values from the data created by that reader function, also I made a
subclass of dict because I needed the _explicit_ functionality of being able to reorder the keys. Yes, it did impact the
run time by a lot, it's O(n).

### Added

##### To Utilities

- **MoveableDict Class**: Custom dictionary subclass supporting `move_to_top` and `move_to_bottom` for key reordering.
- **CSV Reader**: Hand-coded reader(I think the technical term is parser) in `Python_Utilities.py` that handles
  trailing commas and automated line numbering (basically `csv.reader` but better and customized to me :)
- **Search**: Added `dict_search` utility supporting lambda-based data filtering.

### Changed

- **Refactored Utilities**: Moved `copy_dict` to a `@staticmethod` ~~for better memory efficiency and logical
  separation.~~ TO SHUT THE FUCK UP OUT OF MY LINTER (no but it's great guys really helpful). Did end up learning what
  `@override` and `@staticmethod` is. Also got a refresher on Abstract Classes

---

**5th March 2026**

yes, a whole month I unknowingly spent on card_engine. but to be fair, I learnt more from that one project than I ever
will ever learn from a single source ever again. Even In Hindsight, completely worth it, my favourite project ever. like
GOD DAMN I LEARNT SO FUCKING MUCH FROM ONE DAMN PROJECT ITS INSANE. The level difference is very clearly visible when
compared to other projects from before that.

1) new card_engine(PLEASE PLEASE PLEASE CHECK THIS OUT)
2) complete structure update
3) added the tests(still incomplete) for card_engine

---

**16th February 2026**

1) untracked utils folder (haha surely a perfectly nice decision...)
2) updated gitignore a bunch
3) better caeser cipher.

(I swear that's it that's all the commit message says, and I promise that's the LAST time I "fix" caesar_cipher, I
remember changing that 100 times under different commit messages.)

---

**15th February 2026**

1) Finally Learnt What Git Is, How It Works.
2) A LOT OF FOLDER MANAGEMENT
3) obsessed with patching up caesar_cipher code even tho 99% of it is cloned from another repo (check file)
4) Namechanges, stopped using spaces everywhere because, obviously??? young (old??? old me or young me?) was dumb.

---

**14th February 2026**

1) Initial Repo Creation

---

**Note:** there is probably (definitely) a proper and more standard way of writing changelogs, I'll update this the
second I discover it.

This Is The Changelog. (shocking, ik)
