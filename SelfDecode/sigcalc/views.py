import json

from django.http import HttpResponse, HttpResponseBadRequest
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
            post = dict()
            for key, val in request.POST.items():
                if key != 'csrfmiddlewaretoken':
                    post[key] = int(val)

            # Calculate not converted
            notconverted = self._get_notconverted(post)

            if post['convertedA'] > post['visitorsA'] or post['convertedB'] > post['visitorsB']:
                return HttpResponseBadRequest(
                    content=b'Number of visitors cannot be higher than number of conversions.')

            # Generate observed
            observed = np.array([[notconverted['A'], post['convertedA']], [notconverted['B'], post['convertedB']]])

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
        notconvA = post['visitorsA'] - post['convertedA']
        notconvB = post['visitorsB'] - post['convertedB']

        return {'A': notconvA, 'B': notconvB}
