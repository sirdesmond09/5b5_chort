class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model = User

        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    
    def save(self):
        user = User(
            email = self.validated_data["email"],
            username = self.validated_data["email"]
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Response": "Both passwords don't match"})
        user.set_password(password)
        user.save()
        return user