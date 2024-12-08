from django import forms


class MovieReviewForm(forms.Form):
    rating = forms.IntegerField(label="Calificacion", min_value=1, max_value=100, required=True)
    title = forms.CharField(label="Titulo", required=True)
    review = forms.CharField(label="Reseña", min_length=20, required=True)
    widget =  forms.Textarea(attrs={"class": "block w-full rounded-md bg-white px-3" 
                                  "py-1.5 text-base text-gray-900 outline outline-1"
                                  "-outline-offset-1 outline-gray-300 placeholder:text-zinc-400" 
                                  "focus:outline focus:outline-2 focus:-outline-offset-2" 
                                  "focus:outline-amber-400 sm:text-sm/6"})
    title.widget.attrs.update({"class": "py-1.5 pl-3 pr-2 block w-full rounded-md bg-white px-3" 
                                  "py-1.5 text-base text-zinc-900 outline outline-1"
                                  "focus:outline-amber-400 sm:text-sm/6"})
    rating.widget.attrs.update({"class": "rounded-md bg-white py-1.5 pl-3 pr-2 text-base text-zinc-900 outline outline-1 -outline-offset-1 outline-zinc-400 focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-amber-400 sm:text-sm/6"})
    review.widget.attrs.update({"class": "py-1.5 pl-3 pr-2 block w-full rounded-md bg-white px-3" 
                                  "py-1.5 text-base text-zinc-900 outline outline-1"
                                  "focus:outline-amber-400 sm:text-sm/6"})