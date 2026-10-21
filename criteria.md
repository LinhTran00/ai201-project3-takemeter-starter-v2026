# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall Accuracy

<!-- Your criterion. It must name a number. -->
Overall accuracy is at least 0.80 on the held-out set, on all three seeds.


**Why this target:**
My two labels mostly differ in things you can see in the text: `informative`
posts have numbers (prices, times, distances) and descriptions of places, and
`quick_take` posts are short and leave those out. So the model should get most
posts right. I don't expect much more than 0.80, because my hardest boundary
(short posts that name a place, or give an opinion without saying why) is hard
even for me, and those posts will make up most of the errors. I'm setting this
before labelling, so I don't know my label counts yet. If one label ends up
much bigger than the other, a model that always guesses it could also score
near 0.80, so I'll compare against that baseline once my data is labelled.


---

## 2. Consistency

<!-- Your criterion. -->
When someone else labels 30 randomly chosen posts from my dataset using only
my written label definitions and decision rule, we agree on at least 24 of 30
(80%).


**Why this target:**
My labels are only useful if my rule is clear enough for anyone to apply, not
just me. With only two labels and a decision rule built on something you can
point to in the post (one concrete, checkable detail makes it `informative`),
another person should match me on most posts. I didn't go higher because my
hardest boundary, short posts that name a place or give an opinion without
saying why, is where I hesitated most while reading, and someone new to my
rule will likely hesitate there too. If we disagree on more than 6 of 30, my
written rule isn't clear enough, and the model is learning from labels that
depend on who did the labelling.



---

## 3. Per-label performance

<!-- Your criterion. -->
`informative` has an F1 of at least 0.65 on the held-out set, on all three
seeds.


**Why this target:**
From my reading, long, detailed posts with numbers and place descriptions are
less common than quick replies, so I expect `informative` to be my smaller
label. A smaller label has fewer examples in the test split, so its F1 will
jump around more between seeds, and I set it lower than my 0.80 overall target.
I didn't go below 0.65 because `informative` posts have clear signals the model
can learn (numbers, prices, travel times, named streets). If it can't
reliably catch those, it isn't doing the job.



---

## 4. Balance

<!-- Your criterion. -->
`informative` makes up at least 30% of my labelled dataset.


**Why this target:**
I expect `informative` to be my smaller label. If it falls below 30%, always
guessing `quick_take` would score over 0.70 accuracy, which leaves my 0.80
overall target too close to a model that learned nothing. A small
`informative` share also means very few test examples, which makes the F1 in
criterion #3 even jumpier. If I come in under 30%, I'll collect more detailed
posts before training.



---

## 5. Confidence

<!-- Your criterion. -->
Predictions with confidence above 0.70 are correct at least 90% of the time,
on all three seeds.


**Why this target:**
Most of my posts have clear signals: numbers and place descriptions for
`informative`, or a short reply with neither for `quick_take`. The model should
be sure about those, and right. Its mistakes should mostly fall on my hardest
boundary, short posts that name a place or give an opinion without saying why,
and it should be less sure there. If confident predictions are only as accurate
as my 0.80 overall, then the model's confidence tells me nothing about which
predictions to trust.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
