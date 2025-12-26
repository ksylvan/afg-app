import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      credentials: {
        email: { type: "email" }
      },
      authorize: async (credentials) => {
        if (!credentials?.email || typeof credentials.email !== "string") {
          return null
        }

        return {
          id: credentials.email,
          email: credentials.email,
          name: credentials.email.split("@")[0],
        }
      }
    })
  ],
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60,
  },
  jwt: {
    maxAge: 30 * 24 * 60 * 60,
  },
  callbacks: {
    async jwt({ token, user, trigger, session }) {
      if (user) {
        token.id = user.id
        token.email = user.email
        token.name = user.name
      }
      if (trigger === "update" && session) {
        token = { ...token, ...session }
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
        session.user.email = token.email as string
        session.user.name = token.name as string
      }
      return session
    },
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user
      const isOnLoginPage = nextUrl.pathname.startsWith("/login")
      if (isOnLoginPage) {
        if (isLoggedIn) return Response.redirect(new URL("/", nextUrl))
        return true
      }
      return true
    }
  },
  events: {
    async signIn({ user }) {
      console.log(`User signed in: ${user.email}`)
    }
  }
})
