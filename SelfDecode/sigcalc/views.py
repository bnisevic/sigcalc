import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

import numpy as np
from scipy.stats import chi2_contingency


class SigcalcView(TemplateView):

    template_name = 'sigcalc.html'

    def post(self, request, *args, **kwargs):
        """
        If request is ajax throw calculation results in JSON.

        :param request:
        :return:
        """
        if request.is_ajax():
            post = request.POST

            # Calculate not converted
            notconverted = self._get_notconverted(post)

            # Generate observed
            converted_a = int(post['convertedA'])
            converted_b = int(post['convertedB'])
            observed = np.array([[notconverted['A'], converted_a], [notconverted['B'], converted_b]])

            # Get result
            result = chi2_contingency(observed)
            chisq, p = result[:2]

            significance = 'No'
            if p <= 0.05:
                significance = 'Yes'

            result = {'pvalue': round(p, 2), 'significance': significance}

            return HttpResponse(json.dumps(result))

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    @staticmethod
    def _get_notconverted(post):
        """
        Calculate not converted for A and B

        :param post: Data from the AJAX request.
        :return:
        """
        notconvA = int(post['visitorsA']) - int(post['convertedA'])
        notconvB = int(post['visitorsB']) - int(post['convertedB'])

        return {'A': notconvA, 'B': notconvB}
