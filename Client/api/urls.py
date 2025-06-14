from django.urls import path
from .views import (
    ProjectProposalCreateView,
    MyProposalsListView,
    AllProposalsView,
    ApproveProjectProposalView
)

urlpatterns = [
    path("propose/", ProjectProposalCreateView.as_view(), name="propose-project"),
    path("my_proposals/", MyProposalsListView.as_view(), name="my-proposals"),
    path("approve/<uuid:pk>/", ApproveProjectProposalView.as_view(), name="approve-project"),
    path("proposals/", AllProposalsView.as_view(), name="all-proposals"),
]
