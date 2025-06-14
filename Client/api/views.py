from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from ..models import Project, Client
from .serializers import ProjectProposalSerializer, ClientSerializer
from Team.models import Employee


class IsSupervisor(permissions.BasePermission):
    """
    Custom permission to allow only employees with role 'supervisor'.
    """

    def has_permission(self, request, view):
        try:
            employee = request.user.team_employee
            print(employee.role)
            return employee.role.lower() == 'supervisor'
        except Employee.DoesNotExist:
            return False


class ProjectProposalCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyProposalsListView(generics.ListAPIView):
    serializer_class = ProjectProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class AllProposalsView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisor]


class ApproveProjectProposalView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectProposalSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisor]

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.is_approved:
            return Response({"detail": "Already approved."}, status=status.HTTP_400_BAD_REQUEST)

        user = project.user

        # Check if user already has a client
        client = getattr(user, 'client', None)

        if not client:
            client = Client.objects.create(
                fname=project.fname,
                lname=project.lname,
                phone=project.phone,
                email=project.email,
                company=project.company,
                user=user
            )

        project.client = client
        project.is_approved = True
        project.save()

        return Response({"detail": "Proposal approved and client assigned."}, status=status.HTTP_200_OK)
