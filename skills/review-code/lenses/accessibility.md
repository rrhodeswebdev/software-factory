# Lens: accessibility - can everyone use it

Runs only when the diff touches UI.

- Native elements for their job: a button is a `button`, a link is an `a`.
- Every input, icon button and image has an accessible name or alt text.
- Everything works with the keyboard alone, in a sensible order, with visible focus.
- Dialogs, menus and route changes move focus and return it.
- Text contrast at least 4.5:1 (3:1 for large text); meaning never carried by color alone.
- Form errors tied to their field and announced.
- Motion respects reduced-motion settings.
- Mobile: touch targets at least 44 by 44 points; screen-reader labels on native components.
