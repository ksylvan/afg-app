"use client";

import { signIn } from "next-auth/react";
import { useState, type FormEvent } from "react";

export default function LoginPage() {
	const [email, setEmail] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [showSuccess, setShowSuccess] = useState(false);

	const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (!email) return;

		setIsLoading(true);

		try {
			const result = await signIn("credentials", {
				email,
				redirect: false,
			});

			if (result?.ok) {
				setShowSuccess(true);
			} else {
				console.error("Sign in failed:", result?.error);
			}
		} catch (error) {
			console.error("Sign in error:", error);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-amber-600 px-4 py-16 md:py-24">
			<div className="container mx-auto">
				<div className="mx-auto max-w-md">
					<div className="rounded-lg bg-white p-8 shadow-lg md:p-10">
						<h1 className="mb-6 text-3xl font-bold text-blue-900">Sign In</h1>

						{showSuccess ? (
							<div className="rounded-lg bg-green-50 border-l-4 border-green-500 p-6">
								<div className="flex items-start">
									<svg
										className="h-6 w-6 text-green-500 mr-3 mt-0.5"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
									>
										<title>Success checkmark</title>
										<path
											strokeLinecap="round"
											strokeLinejoin="round"
											strokeWidth={2}
											d="M5 13l4 4L19 7"
										/>
									</svg>
									<div>
										<h3 className="text-lg font-semibold text-green-800">
											Magic link sent to your email
										</h3>
										<p className="mt-2 text-sm text-green-700">
											Check your inbox and click the link to sign in. The link
											will expire in 30 days.
										</p>
									</div>
								</div>
							</div>
						) : (
							<form onSubmit={handleSubmit} className="space-y-6">
								<div>
									<label
										htmlFor="email"
										className="block mb-2 text-sm font-medium text-gray-700"
									>
										Email Address
									</label>
									<input
										id="email"
										type="email"
										value={email}
										onChange={(e) => setEmail(e.target.value)}
										required
										className="w-full rounded-lg border border-gray-300 px-4 py-3 text-gray-900 transition-colors focus:border-amber-500 focus:ring-2 focus:ring-amber-500 focus:outline-none"
										placeholder="you@example.com"
										disabled={isLoading}
									/>
								</div>

								<button
									type="submit"
									disabled={isLoading || !email}
									className="w-full rounded-lg bg-amber-500 px-6 py-3 font-semibold text-white shadow-lg transition-colors hover:bg-amber-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
								>
									{isLoading ? "Sending..." : "Send Magic Link"}
								</button>
							</form>
						)}

						<div className="mt-6 text-center text-sm text-gray-600">
							<p className="mb-2">
								<span className="font-medium">Note:</span> No password required
							</p>
							<p className="text-xs text-gray-500">
								You will receive a secure link to sign in without a password
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}
